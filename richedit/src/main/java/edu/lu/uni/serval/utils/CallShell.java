package edu.lu.uni.serval.utils;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.concurrent.TimeUnit;

/**
 * Created by anilkoyuncu on 17/04/2018.
 */
public class CallShell
{
    private static final Logger log = LoggerFactory.getLogger(CallShell.class);

    public void runShell(String command) throws Exception
    {
        Process process = Runtime.getRuntime().exec(command);
        BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
        String s;
        while ((s = reader.readLine()) != null)
        {
            System.out.println("Script output: " + s);
        }
    }

    public static void runShell(String command, String port) throws Exception
    {
        log.trace(command);

        Process process = Runtime.getRuntime().exec(command);
        BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
        String s;
        while ((s = reader.readLine()) != null)
        {
            log.trace("Script output: " + s);
        }

        String cmd = "redis-cli -p %s ping";
        String cmd1 = String.format(cmd, Integer.valueOf(port));
        runPing(cmd1);
    }

    public static void runPing(String command) throws Exception
    {
        try
        {
            StringBuffer output = new StringBuffer();
            Process process = Runtime.getRuntime().exec(command);
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            String s;

            BufferedReader stdError = new BufferedReader(new InputStreamReader(process.getErrorStream()));

            s = reader.readLine();

            if (s != null && s.equals("PONG"))
            {
                log.trace(s);
            }
            else
            {
                String e;
                if ((e = stdError.readLine()) == null)
                {
                    TimeUnit.MINUTES.sleep(1);

                    runPing(command);
                }
                else
                {
                    TimeUnit.MINUTES.sleep(1);
                    System.out.println(e);
                }
            }

            while ((s = stdError.readLine()) != null)
                System.out.print(s);
        }
        catch (IOException e)
        {
            System.out.println("exception happened - here's what I know: ");
            e.printStackTrace();
            System.exit(-1);
        }
    }
}

