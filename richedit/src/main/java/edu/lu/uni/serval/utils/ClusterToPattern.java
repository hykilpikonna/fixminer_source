package edu.lu.uni.serval.utils;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPool;


public class ClusterToPattern
{
    private static final Logger log = LoggerFactory.getLogger(ClusterToPattern.class);

    public static void main(String port, String redisPath, String dumpsName, String parameter) throws Exception
    {
        CallShell cs = new CallShell();
        String cmd = "bash " + redisPath + "/" + "startServer.sh" + " %s %s %s";
        cmd = String.format(cmd, redisPath, dumpsName, Integer.valueOf(port));
        log.trace(cmd);
        CallShell.runShell(cmd, port);
        String host = "localhost";//args[5];
        final JedisPool outerPool = new JedisPool(PoolBuilder.getPoolConfig(), host, Integer.parseInt(port), 20000000);
        String export = export(parameter, outerPool);
        System.out.println(export);
    }

    private static String export(String filename, JedisPool outerPool)
    {
        try (Jedis outer = outerPool.getResource())
        {
            while (!outer.ping().equals("PONG")) log.info("wait");
            return outer.hget("dump", filename);
        }
    }
}
