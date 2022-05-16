package edu.lu.uni.serval.richedit.jobs;

import edu.lu.uni.serval.utils.CallShell;
import edu.lu.uni.serval.utils.EDiffHelper;
import edu.lu.uni.serval.utils.PoolBuilder;
import me.tongfei.progressbar.ProgressBar;
import org.apache.commons.text.similarity.JaroWinklerDistance;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPool;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

/**
 * Created by anilkoyuncu on 03/04/2018.
 */
public class CompareTrees
{
    private static final Logger log = LoggerFactory.getLogger(CompareTrees.class);

    public static void main(String redisPath, String port, String dumpsName, String numOfWorkers) throws Exception
    {
        final JedisPool outerPool = new JedisPool(PoolBuilder.getPoolConfig(), "localhost", Integer.parseInt(port), 20000000);

        HashMap<String, String> filenames = getFilenames(outerPool);
        String job = getLevel(outerPool);

        ArrayList<String> errorPairs = new ArrayList<>();

        Long compare;
        try (Jedis inner = outerPool.getResource())
        {
            compare = inner.scard("compare");
        }
        IntStream stream = IntStream.range(0, compare.intValue());

        ProgressBar.wrap(stream.parallel(), "Task").forEach(m ->
            {
                newCoreCompare(job, errorPairs, filenames, outerPool);
            }
        );

        log.info("End process");
    }

    public static boolean newCoreCompare(String treeType, ArrayList<String> errorPairs, HashMap<String, String> filenames, JedisPool outerPool)
    {
        String pairName = null;
        try (Jedis outer = outerPool.getResource())
        {
            pairName = outer.spop("compare");
            //        }
            if (pairName.equals("0"))
            {
                return true;
            }
            String matchKey = null;

            String[] split = pairName.split("/");

            String i = split[1];
            String j = split[2];
            String keyName = split[0];
            matchKey = keyName + "/" + (i) + "/" + j;

            if (matchKey == null)
            {
                return false;
            }
            Map<String, String> oldTreeString = EDiffHelper.getTreeString(keyName, i, outerPool, filenames);
            Map<String, String> newTreeString = EDiffHelper.getTreeString(keyName, j, outerPool, filenames);

            switch (treeType)
            {
                case "single":


                    String oldShapeTree = oldTreeString.get("shapeTree");
                    String newShapeTree = newTreeString.get("shapeTree");

                    String oldActionTree = oldTreeString.get("actionTree");
                    String newActionTree = newTreeString.get("actionTree");

                    String oldTargetTree = oldTreeString.get("targetTree");
                    String newTargetTree = newTreeString.get("targetTree");


                    if (oldShapeTree.equals(newShapeTree))
                    {
                        if (oldActionTree.equals(newActionTree))
                        {
                            if (oldTargetTree.equals(newTargetTree))
                            {
                                try (Jedis jedis = outerPool.getResource())
                                {
                                    jedis.select(2);
                                    jedis.set(matchKey, "1");
                                }
                            }
                        }
                    }
                    return true;
                case "token":

                    String oldTokens = oldTreeString.get("tokens");
                    String newTokens = newTreeString.get("tokens");

                    JaroWinklerDistance jwd = new JaroWinklerDistance();
                    Double overallSimi = Double.valueOf(0);
                    if (!(oldTokens.trim().isEmpty() || newTokens.trim().isEmpty()))
                    {
                        overallSimi = jwd.apply(oldTokens, newTokens);
                    }
                    int retval = Double.compare(overallSimi, Double.valueOf(1));

                    if (retval >= 0)
                    {
                        try (Jedis jedis = outerPool.getResource())
                        {
                            jedis.select(3);
                            jedis.set(matchKey, "1");
                        }
                    }
                    return true;
                default:
                    return true;
            }
        }
        catch (Exception e)
        {
            errorPairs.add(pairName);
            if (pairName == null) return false;
            log.debug("{} not comparable", pairName);
        }

        return true;
    }

    public static String getLevel(JedisPool innerPool)
    {
        HashMap<String, String> fileMap = new HashMap<String, String>();

        try (Jedis inner = innerPool.getResource())
        {
            while (!inner.ping().equals("PONG"))
            {
                log.info("wait");
            }

            inner.select(1);
            String level = inner.get("level");

            switch (level)
            {
                case "l1":
                    return "single";
                case "l2":
                    return "token";
                default:
                    return "";
            }
        }
    }

    public static HashMap<String, String> getFilenames(JedisPool innerPool)
    {
        HashMap<String, String> fileMap = new HashMap<String, String>();

        try (Jedis inner = innerPool.getResource())
        {
            while (!inner.ping().equals("PONG"))
            {
                log.info("wait");
            }

            inner.select(1);
            Map<String, String> filenames = inner.hgetAll("filenames");

            for (Map.Entry<String, String> stringStringEntry : filenames.entrySet().stream().collect(Collectors.toList()))
            {
                fileMap.put(stringStringEntry.getKey(), stringStringEntry.getValue());
            }
        }

        return fileMap;
    }
}
