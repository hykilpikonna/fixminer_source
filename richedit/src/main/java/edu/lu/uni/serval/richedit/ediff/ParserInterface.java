package edu.lu.uni.serval.richedit.ediff;

public interface ParserInterface
{


    //	public void parseFixPatterns(File prevFile, File revFile, File diffEntryFile);

    String getAstEditScripts();

    String getPatchesSourceCode();

    //	public String getBuggyTrees();

    String getSizes();

    String getTokensOfSourceCode();

    //	public String getOriginalTree();

    //	public String getActionSets();
}
