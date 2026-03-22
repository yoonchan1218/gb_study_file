package com.example.mysql.domain;

import com.example.mysql.audit.Period;
import lombok.*;
import lombok.experimental.SuperBuilder;
import org.springframework.stereotype.Component;

@Component
@Getter @ToString
@EqualsAndHashCode(of="id")
@SuperBuilder
public class PostVO extends Period {
    private Long id;
    private String postTitle;
    private String postContent;
    private int postReadCount;
    private Long memberId;
}








