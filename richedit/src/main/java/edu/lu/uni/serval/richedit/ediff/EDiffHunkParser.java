package edu.lu.uni.serval.richedit.ediff;

import com.github.gumtreediff.tree.ITree;
import edu.lu.uni.serval.utils.EDiffHelper;
import edu.lu.uni.serval.utils.Timer;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPool;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;
import java.util.concurrent.TimeoutException;


/**
 * Parse fix violations with GumTree in terms of multiple statements.
 *
 * @author kui.liu
 */
public class EDiffHunkParser extends EDiffParser
{
    private static final Logger logger = LoggerFactory.getLogger(EDiffHunkParser.class);

    @Override
    public void parseFixPatterns(File prevFile, File revFile, File diffentryFile, String project,
                                 JedisPool innerPool, String srcMLPath, String hunkLimit, boolean isJava)
    {
        int hunkSize = Integer.parseInt(hunkLimit);
        Path prevpath = Paths.get(prevFile.getPath());
        Path revpath = Paths.get(prevFile.getPath());
        Path diffpath = Paths.get(diffentryFile.getPath());
//        try
//        {
//            if (((Files.size(prevpath) / 1024.0) > 7) || ((Files.size(revpath) / 1024.0) > 7) || ((Files.size(diffpath) / 1024.0) > 1)){
//               // logger.info("bigfile {}, skipping...", prevFile);
//                return;
//            }
//        }
//        catch (IOException e)
//        {
//            throw new RuntimeException(e);
//        }
        //        if (!prevFile.getPath().equals("/workspace/EECS-Research/data/0/patches/camel/prevFiles/prev_0da32d_a27076_components#camel-jclouds#src#main#java#org#apache#camel#component#jclouds#JcloudsBlobStoreProducer.java"))
//            return;

//        Timer timer = new Timer();
//
//        logger.info("prevfile {}", prevFile);
//        logger.info("revfile {}", revFile);
//        logger.info("diffentryFile {}", diffentryFile);

        try
        {
            String[] split1 = diffentryFile.getParent().split(project);
            String pj = split1[1].split("/")[1];

            List<HierarchicalActionSet> actionSets = parseChangedSourceCodeWithGumTree2(prevFile, revFile, srcMLPath, isJava);

            if (actionSets == null || actionSets.size() == 0 || actionSets.size() > hunkSize) return;

            int hunkSet = 0;
            for (HierarchicalActionSet actionSet : actionSets)
            {
                String astNodeType = actionSet.getAstNodeType();
//                actionSet.toString();
                // Size limit (due to large trees generated for unknown reason)
                int maxSize = 100;
                int size = actionSet.getActionSizeRec(maxSize);
                if (size > maxSize) continue;
//                System.out.println(size);
                // timer.log("getActionSizeRec, size = " + size);
//                int size = actionSet.strList.size();
                String key = astNodeType + "/" + size + "/" + pj + "_" + diffentryFile.getName() + "_" + hunkSet;
                ITree targetTree = EDiffHelper.getTargets(actionSet, isJava);
                // timer.log("getTargets");
                ITree actionTree = EDiffHelper.getActionTrees(actionSet);
                // timer.log("getActionTrees");
                ITree shapeTree = EDiffHelper.getShapeTree(actionSet, isJava);
                // timer.log("getShapeTree");
                ITree tokenTree = EDiffHelper.getTokenTree(actionSet, isJava);
                // timer.log("getTokenTree");
                String tokens = EDiffHelper.getNames2(tokenTree);
                // timer.log("getNames2");
                try (Jedis inner = innerPool.getResource())
                {
                    inner.hset("dump", key, actionSet.toString());
//                    inner.hset("dump", key, "");
                    inner.hset(key, "actionTree", actionTree.toStaticHashString());
                    inner.hset(key, "targetTree", targetTree.toStaticHashString());
                    inner.hset(key, "shapeTree", shapeTree.toStaticHashString());
                    inner.hset(key, "tokens", tokens);
                }
                // timer.log("dump");

                hunkSet++;
            }
            try (Jedis inner = innerPool.getResource())
            {
                inner.hset("diffEntry", pj + "_" + diffentryFile.getName(), "1");
            }
           // logger.info("Finished processing {}", prevFile);
        }

        catch (Exception e)
        {
            logger.error("error", e);
        }
    }
}
