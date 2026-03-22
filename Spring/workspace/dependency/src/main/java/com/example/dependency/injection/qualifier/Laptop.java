package com.example.dependency.injection.qualifier;

import org.springframework.context.annotation.Primary;
import org.springframework.stereotype.Component;

@Component
@Primary
//@Qualifier("laptop")
public class Laptop implements Computer {
    @Override
    public int getScreenWidth() {
        return 1280;
    }
}
