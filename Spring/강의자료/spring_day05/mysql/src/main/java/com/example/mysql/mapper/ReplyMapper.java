package com.example.mysql.mapper;

import com.example.mysql.domain.ReplyVO;
import com.example.mysql.dto.ReplyDTO;
import org.apache.ibatis.annotations.Mapper;

import java.util.Optional;

@Mapper
public interface ReplyMapper {
//    댓글 작성 후

//    답글이 1개라도 있으면, "삭제된 댓글입니다" 표시
//    답글이 0개라면, 삭제

//    추가
    public void insert(ReplyVO replyVO);
    public void insertReReply(ReplyVO replyVO);
    public int selectDepth(Long parentId);
//    목록
//    조회
    public Optional<ReplyDTO> selectById(Long id);
//    수정
//    삭제
}











