package edu.lu.uni.serval.richedit.ediff;

import com.github.gumtreediff.actions.model.Action;
import com.github.gumtreediff.gen.srcml.GumTreeCComparer;
import edu.lu.uni.serval.gumtree.GumTreeComparer;
import edu.lu.uni.serval.utils.ListSorter;
import redis.clients.jedis.JedisPool;

import java.io.File;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;

/**
 * Parse fix patterns with GumTree.
 *
 * @author kui.liu
 */
public class EDiffParser extends Parser
{

    /*
     * ResultType:
     * 0: normal GumTree results.
     * 1: null GumTree result.
     * 2: No source code changes.
     * 3: No Statement Change.
     * 4: useless violations
     */
    public int resultType = 0;


    /**
     * Regroup GumTree results without remove the modification of variable names.
     *
     * @param prevFile
     * @param revFile
     * @return
     */
    public List<HierarchicalActionSet> parseChangedSourceCodeWithGumTree2(File prevFile, File revFile, String srcMLPath, boolean isJava)
    {
        List<HierarchicalActionSet> actionSets = new ArrayList<>();
        List<Action> gumTreeResults = null;
        if (isJava)
        {
            gumTreeResults = new GumTreeComparer().compareTwoFilesWithGumTree(prevFile, revFile);
        }
        else
        {
            gumTreeResults = new GumTreeCComparer().compareCFilesWithGumTree(prevFile, revFile, srcMLPath);
        }
        if (gumTreeResults == null)
        {
            this.resultType = 1;
            return actionSets;
        }
        else if (gumTreeResults.size() == 0)
        {
            this.resultType = 2;
            return actionSets;
        }
        else
        {
            // Regroup GumTre results.
            List<HierarchicalActionSet> allActionSets = null;
            if (isJava)
            {
                allActionSets = new HierarchicalRegrouper().regroupGumTreeResults(gumTreeResults);
            }
            else
            {
                HashSet<Integer> removeType = new HashSet<Integer>(Arrays.asList(131, 132, 133, 134, 135, 136, 137));
                boolean b = gumTreeResults.stream().anyMatch(p -> removeType.contains(p.getNode().getType()));
                if (b)
                {
                    return actionSets;
                }
                allActionSets = new HierarchicalRegrouperForC().regroupGumTreeResults(gumTreeResults);
            }


            ListSorter<HierarchicalActionSet> sorter = new ListSorter<>(allActionSets);
            actionSets = sorter.sortAscending();

            if (actionSets.size() == 0)
            {
                this.resultType = 3;
            }

            return actionSets;
        }
    }

    @Override
    public void parseFixPatterns(File prevFile, File revFile, File diffEntryFile, String project, JedisPool innerPool, String srcMLPath, String rootType, boolean isJava)
    {

    }

    //	@Override
    //	public void parseFixPatterns(File prevFile, File revFile, File diffEntryFile, String project, JedisPool innerPool) {
    //
    //	}
}
