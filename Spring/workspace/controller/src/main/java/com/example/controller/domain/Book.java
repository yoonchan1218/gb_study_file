package com.example.controller.domain;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.ToString;

@NoArgsConstructor
@Getter @Setter @ToString
public class Book {
    private String title;
    private String author;
    private int price;
    private String publisher;

    public double bookSale(){
        return (double)price*0.9;
    }

}
