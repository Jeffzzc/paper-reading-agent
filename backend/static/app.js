const { createApp, ref, computed, onMounted } = Vue;

createApp({
    setup() {
        const inputType = ref('url');
        const inputValue = ref(''); // Default for testing
        const loading = ref(false);
        const currentTask = ref(null);
        const result = ref(null);
        const history = ref([]);
        let pollInterval = null;

        const progressPercentage = computed(() => {
            if (!currentTask.value) return 0;
            const status = currentTask.value.status;
            switch(status) {
                case 'pending': return 10;
                case 'searching': return 30;
                case 'analyzing': return 50;
                case 'code_analyzing': return 70;
                case 'summarizing': return 90;
                case 'completed': return 100;
                case 'failed': return 100;
                default: return 0;
            }
        });

        const formatDate = (dateString) => {
            if (!dateString) return '';
            return new Date(dateString).toLocaleDateString();
        };

        const analyzePaper = async () => {
            if (!inputValue.value) return;
            
            loading.value = true;
            result.value = null;
            currentTask.value = null;

            try {
                const response = await axios.post('/api/analyze', {
                    input_type: inputType.value,
                    value: inputValue.value
                });
                
                currentTask.value = response.data;
                startPolling(response.data.task_id);
                
            } catch (error) {
                console.error("Error starting analysis:", error);
                alert("Failed to start analysis");
                loading.value = false;
            }
        };

        const startPolling = (taskId) => {
            if (pollInterval) clearInterval(pollInterval);
            
            pollInterval = setInterval(async () => {
                try {
                    const response = await axios.get(`/api/status/${taskId}`);
                    currentTask.value = response.data;
                    
                    if (['completed', 'failed'].includes(response.data.status)) {
                        clearInterval(pollInterval);
                        loading.value = false;
                        if (response.data.status === 'completed') {
                            result.value = response.data.result;
                            fetchHistory();
                        } else {
                            alert(`Analysis failed: ${response.data.message}`);
                        }
                    }
                } catch (error) {
                    console.error("Polling error:", error);
                    clearInterval(pollInterval);
                    loading.value = false;
                }
            }, 2000);
        };
        
        const fetchHistory = async () => {
            try {
                const response = await axios.get('/api/history');
                history.value = response.data.reverse();
            } catch (error) {
                console.error("Error fetching history:", error);
            }
        };

        const loadTask = (task) => {
            currentTask.value = task;
            if (task.status === 'completed') {
                result.value = task.result;
            }
        };

        onMounted(() => {
            fetchHistory();
        });

        return {
            inputType,
            inputValue,
            loading,
            currentTask,
            result,
            history,
            progressPercentage,
            analyzePaper,
            formatDate,
            loadTask
        };
    }
}).mount('#app');
