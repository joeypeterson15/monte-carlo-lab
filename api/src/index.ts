import cors from '@fastify/cors'
import Fastify from 'fastify'
import { Redis } from 'ioredis'

const port = Number(process.env.PORT ?? 3000)
const host = process.env.HOST ?? '0.0.0.0'
const redisUrl = process.env.REDIS_URL ?? 'redis://127.0.0.1:6379/0'
const workerQueue = process.env.WORKER_QUEUE ?? 'jobs'
const corsOrigin = process.env.CORS_ORIGIN ?? true

const redis = new Redis(redisUrl, { maxRetriesPerRequest: null })

const app = Fastify({ logger: true })

await app.register(cors, { origin: corsOrigin })

app.get('/health', async (_request, reply) => {
  try {
    const pong = await redis.ping()
    if (pong !== 'PONG') {
      reply.code(503)
      return { status: 'unavailable' }
    }
    return { status: 'ok' }
  } catch {
    reply.code(503)
    return { status: 'unavailable' }
  }
})

app.addHook('onClose', async () => {
  if (redis.status === 'end') return
  await redis.quit()
})

for (const signal of ['SIGINT', 'SIGTERM'] as const) {
  process.on(signal, () => {
    void app.close()
  })
}

try {
  await app.listen({ port, host })
  app.log.info({ workerQueue }, 'redis worker channel configured')
} catch (error) {
  app.log.error(error)
  process.exit(1)
}
