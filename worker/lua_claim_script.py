claim_script = """-- KEYS[1] = "queue:jobs"
-- ARGV[1] = worker id (e.g. "worker-3")
-- ARGV[2] = lease TTL in seconds (e.g. 15)

-- 1. Pop the next chunk command (a JSON string). The coordinator pushes with RPUSH.
local raw = redis.call('LPOP', KEYS[1])

if not raw then
  return nil
end

local chunk = cjson.decode(raw)
local lease_key    = 'lease:' .. chunk.job_id .. ':' .. chunk.chunk_id
local inflight_key = 'job:' .. chunk.job_id .. ':inflight'

redis.call('SET', lease_key, ARGV[1], 'EX', tonumber(ARGV[2]))

redis.call('HSET', inflight_key, chunk.chunk_id, raw)

-- 6. Hand the chunk back to the worker.
return raw"""