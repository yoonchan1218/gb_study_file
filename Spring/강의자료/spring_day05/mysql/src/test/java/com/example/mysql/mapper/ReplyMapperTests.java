package com.example.mysql.mapper;

import com.example.mysql.dto.ReplyDTO;
import lombok.extern.slf4j.Slf4j;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.util.Optional;

@Slf4j
@SpringBootTest
public class ReplyMapperTests {
    @Autowired
    private ReplyMapper replyMapper;

    @Test
    public void testInsert(){
        ReplyDTO replyDTO = new ReplyDTO();
        replyDTO.setReplyContent("테스트 댓글1");
        replyDTO.setMemberId(2L);
        replyDTO.setReviewId(5L);

        replyMapper.insert(replyDTO.toVO());
    }

    @Test
    public void testInsertReReply(){
        Optional<ReplyDTO> foundReply = replyMapper.selectById(1L);

        foundReply.ifPresent(replyDTO -> {
            log.info(replyDTO.toString());
            ReplyDTO reply = new ReplyDTO();
            reply.setReplyContent("테스트 대댓글2");
            reply.setMemberId(2L);
            reply.setReviewId(5L);
            reply.setParentId(replyDTO.getId());
            reply.setDepth(replyMapper.selectDepth(replyDTO.getId()));
            replyMapper.insertReReply(reply.toVO());
        });

    }
}
















