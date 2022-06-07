package edu.lu.uni.serval.richedit.ediff;

import com.github.gumtreediff.actions.model.Action;
import com.github.gumtreediff.tree.ITree;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;

/**
 * Hierarchical-level results of GumTree results
 *
 * @author kui.liu
 */
public class HierarchicalActionSet implements Comparable<HierarchicalActionSet>, Serializable
{
    private static final Logger log = LoggerFactory.getLogger(EDiffHunkParser.class);

    private String astNodeType;

    private Action action;

    private Action parentAction;

    private String actionString;

    private Integer startPosition;

    private Integer length;

    private int bugStartLineNum = 0;

    private int bugEndLineNum;

    private int fixStartLineNum;

    private int fixEndLineNum;

    private HierarchicalActionSet parent = null;

    private List<HierarchicalActionSet> subActions = new ArrayList<>();

    private ITree node;
    // source code tree.

    public int getBugEndPosition()
    {
        return bugEndPosition;
    }

    public int getFixEndPosition()
    {
        return fixEndPosition;
    }

    private int bugEndPosition;

    private int fixEndPosition;

    public ITree getNode()
    {
        return node;
    }

    public void setNode(ITree node)
    {
        this.node = node;
    }

    public void setAstNodeType(String astNodeType)
    {
        this.astNodeType = astNodeType;
    }

    public String getAstNodeType()
    {
        return astNodeType;
    }

    public Action getAction()
    {
        return action;
    }

    public void setAction(Action action)
    {
        this.action = action;
    }

    public Action getParentAction()
    {
        return parentAction;
    }

    public void setParentAction(Action parentAction)
    {
        this.parentAction = parentAction;
    }

    public String getActionString()
    {
        return actionString;
    }

    public void setActionString(String actionString)
    {
        this.actionString = actionString;

        int atIndex = actionString.indexOf("@AT@") + 4;
        int lengthIndex = actionString.indexOf("@LENGTH@");
        if (lengthIndex == -1)
        {
            this.startPosition = Integer.parseInt(actionString.substring(atIndex).trim());
            this.length = 0;
        }
        else
        {
            this.startPosition = Integer.parseInt(actionString.substring(atIndex, lengthIndex).trim());
            this.length = Integer.parseInt(actionString.substring(lengthIndex + 8).trim());
        }

        String nodeType = actionString.substring(0, actionString.indexOf("@@"));
        nodeType = nodeType.substring(nodeType.indexOf(" ") + 1);
        this.astNodeType = nodeType;
    }

    public int getStartPosition()
    {
        return startPosition;
    }

    public int getLength()
    {
        return length;
    }

    public int getBugStartLineNum()
    {
        return bugStartLineNum;
    }

    public void setBugStartLineNum(int bugStartLineNum)
    {
        this.bugStartLineNum = bugStartLineNum;
    }

    public int getBugEndLineNum()
    {
        return bugEndLineNum;
    }

    public void setBugEndLineNum(int bugEndLineNum)
    {
        this.bugEndLineNum = bugEndLineNum;
    }

    public int getFixStartLineNum()
    {
        return fixStartLineNum;
    }

    public void setFixStartLineNum(int fixStartLineNum)
    {
        this.fixStartLineNum = fixStartLineNum;
    }

    public int getFixEndLineNum()
    {
        return fixEndLineNum;
    }

    public void setFixEndLineNum(int fixEndLineNum)
    {
        this.fixEndLineNum = fixEndLineNum;
    }

    public HierarchicalActionSet getParent()
    {
        return parent;
    }

    public void setParent(HierarchicalActionSet parent)
    {
        this.parent = parent;
    }

    public List<HierarchicalActionSet> getSubActions()
    {
        return subActions;
    }

    public void setSubActions(List<HierarchicalActionSet> subActions)
    {
        this.subActions = subActions;
    }


    public void setBugEndPosition(int bugEndPosition)
    {
        this.bugEndPosition = bugEndPosition;
    }


    public void setFixEndPosition(int fixEndPosition)
    {
        this.fixEndPosition = fixEndPosition;
    }

    @Override
    public int compareTo(HierarchicalActionSet o)
    {

        return this.startPosition.compareTo(o.startPosition);//this.action.compareTo(o.action);
    }

    final List<String> strList = new ArrayList<>();

//    public int getActionSize()
//    {
//        return strList.size();
//    }

    private Integer size = null;

    public int getActionSizeRec(int maxSize)
    {
        if (this.size != null) return this.size;

        int size = 1;
        for (HierarchicalActionSet s : subActions)
        {
            size += s.getActionSizeRec(maxSize);
            if (size > maxSize) return maxSize + 1;
        }

        return this.size = size;
    }

    @Override
    public String toString()
    {
//        log.info("Calling toString on {}", actionString);
        if (strList.size() == 0)
        {
            strList.add(actionString);

            // TODO: Can we use unique subActions instead of full subActions with many duplicates?
//            List<HierarchicalActionSet> usedSubActions = subActions.size() > 20 ? new ArrayList<>(new HashSet<>(subActions)) : subActions;

            for (HierarchicalActionSet actionSet : subActions)
            {
                actionSet.toString();
                for (String str1 : actionSet.strList)
                {
                    strList.add("---" + str1);
                }
            }
        }

        String str = "";
        for (String str1 : strList)
        {
            str += str1 + "\n";
        }

        return str;
    }
}
