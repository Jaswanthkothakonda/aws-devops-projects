package com.beasteats;

import org.apache.commons.lang3.StringUtils;

public class App {

    public static String greeting() {
        return StringUtils.capitalize("hello from BeastEats!");
    }

    public static void main(String[] args) {
        System.out.println(greeting());
        System.out.println("Maven is building our Java application.");
    }
}
