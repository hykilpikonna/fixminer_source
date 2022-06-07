package edu.lu.uni.serval.utils;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Timer
{
    private static final Logger logger = LoggerFactory.getLogger(Timer.class);

    long start = System.nanoTime();

    public void log(String msg)
    {
        long elapse = (long) ((System.nanoTime() - start) / 1e6);
        logger.info("{}ms: {}", elapse, msg);
        start = System.nanoTime();
    }
}
