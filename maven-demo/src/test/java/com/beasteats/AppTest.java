package com.beasteats;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertEquals;

class AppTest {

    @Test
    void greetingReturnsExpectedMessage() {
        assertEquals("Hello from BeastEats!", App.greeting());
    }
}
