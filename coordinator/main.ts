const redisUrl = process.env.REDIS_URL ?? 'redis://127.0.0.1:6379/0'
N_WORKERS = process.env.N_WORKERS

const redis = new Redis(redisUrl, { maxRetriesPerRequest: null })

interface JobPayload {
    name: string;
    iterations: number;
}

class Coordinator {
    constructor(){
    }
    process(payload){
        
        const jobPayload = JSON.parse(payload) as JobPayload
        const { name, iterations } = JobPayload
    }
}



