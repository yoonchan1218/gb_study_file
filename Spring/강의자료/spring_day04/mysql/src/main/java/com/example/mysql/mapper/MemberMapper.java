package com.example.mysql.mapper;

import com.example.mysql.domain.MemberVO;
import org.apache.ibatis.annotations.Mapper;

import java.util.List;
import java.util.Optional;

@Mapper
public interface MemberMapper {
    public void insert(MemberVO memberVO);
    public void insertInactive(MemberVO memberVO);
    public Optional<MemberVO> selectById(Long id);
    public List<MemberVO> selectAll();
    public void updateStatus(Long id);
    public void delete(Long id);
}
