package edu.lu.uni.serval;


import edu.lu.uni.serval.richedit.jobs.CompareTrees;
import edu.lu.uni.serval.richedit.jobs.EnhancedASTDiff;
import edu.lu.uni.serval.utils.ClusterToPattern;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.yaml.snakeyaml.Yaml;

import java.io.FileInputStream;
import java.io.IOException;
import java.util.Map;
import java.util.Properties;

/**
 * Created by anilkoyuncu on 14/04/2018.
 */
public class Launcher
{

    private static Logger log = LoggerFactory.getLogger(Launcher.class);

    public static void main(String[] args) throws IOException
    {
        Properties appProps = new Properties();

        if (args.length != 2)
        {
            System.out.println("Proper Usage is: \n\tfirst argument full path to .properties file (e.g. an example is located under resources) \n\tsecond argument jobType (e.g RICHEDITSCRIPT, COMPARE)");
            System.exit(0);
        }

        String appConfigPath = args[0];

        Yaml yaml = new Yaml();
        Map<String, Object> obj = yaml.load(new FileInputStream(appConfigPath));

        appProps.load(new FileInputStream(appConfigPath));
        Map<String, Object> fixminer = (Map<String, Object>) obj.get("fixminer");
        String numOfWorkers = String.valueOf(fixminer.get("numOfWorkers"));
        String portDumps = String.valueOf(fixminer.get("portDumps"));
        String projectType = (String) fixminer.get("projectType");

        String hunkLimit = String.valueOf(fixminer.get("hunkLimit"));
        String patchSize = String.valueOf(fixminer.get("patchSize"));
        String projectL = (String) fixminer.get("projectList");
        String[] projectList = projectL.split(",");
        String input = (String) fixminer.get("inputPath");
        String redisPath = (String) fixminer.get("redisPath");
        String srcMLPath = (String) fixminer.get("srcMLPath");

        String jobType = args[1];

        mainLaunch(numOfWorkers, jobType, portDumps, projectType, input, redisPath, srcMLPath, hunkLimit, projectList, patchSize);
    }

    public static void mainLaunch(String numOfWorkers, String jobType, String portDumps, String projectType, String input, String redisPath, String srcMLPath, String hunkLimit, String[] projectList, String patchSize)
    {
        String dbDir;
        String dumpsName;
        String gumInput;

        dumpsName = "dumps-" + projectType + ".rdb";

        gumInput = input;
        dbDir = redisPath;

        try
        {
            switch (jobType)
            {
                case "RICHEDITSCRIPT":
                    EnhancedASTDiff.main(gumInput, portDumps, dbDir, dumpsName, srcMLPath, hunkLimit, projectList, patchSize, projectType);
                    break;

                case "COMPARE":
                    CompareTrees.main(redisPath, portDumps, dumpsName, numOfWorkers);
                    break;
                default:
                    throw new Error("unknown Job");
            }
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }
    }
}


