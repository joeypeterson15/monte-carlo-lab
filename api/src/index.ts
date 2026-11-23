import cors from '@fastify/cors'
import Fastify from 'fastify'
import { Redis } from 'ioredis'
import { JsonSchemaToTsProvider } from '@fastify/type-provider-json-schema-to-ts';

const port = Number(process.env.PORT ?? 3000)
const host = process.env.HOST ?? '0.0.0.0'
const redisUrl = process.env.REDIS_URL ?? 'redis://127.0.0.1:6379/0'
const workerQueue = process.env.WORKER_QUEUE ?? 'jobs'
const corsOrigin = process.env.CORS_ORIGIN ?? true
const workers = process.env.N_WORKERS

const redis = new Redis(redisUrl, { maxRetriesPerRequest: null })

const app = Fastify({ logger: true }).withTypeProvider<JsonSchemaToTsProvider>();

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

// Check request body and payload
const runBodySchema = {
  type: 'object',
  properties: {
    name: { type: 'string' },
    iterations: { type: 'number' },
  },
  required: ['name', 'iterations'],
  additionalProperties: false,
} as const;

// Send coordinator payload
// TO DO: Handle coordinator error
app.post('/run', { schema: { body: runBodySchema } }, async (request, reply) => {
  redis.
  reply.code(202)
  return { status: 'submitted'}
});

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
