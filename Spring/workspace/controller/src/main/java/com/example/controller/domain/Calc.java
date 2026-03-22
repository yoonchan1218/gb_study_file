package com.example.controller.domain;

import lombok.*;

@NoArgsConstructor
@Getter @Setter @ToString
//@EqualsAndHashCode(onlyExplicitlyIncluded = true)
public class Calc {
//    @EqualsAndHashCode.Include
    int num1;
    int num2;

    public int getTotal() {
        return num1 + num2;
    }
    public int getMinus(){
        return num1 - num2;
    }
    public int getMultiple(){
        return num1 * num2;
    }
    public double getDivide(){
        return (double)num1 / num2;
    }
}
