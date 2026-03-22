package com.app.member.repository;

import java.util.Optional;

import org.apache.ibatis.session.SqlSession;

import com.app.member.domain.MemberVO;
import com.app.mybatis.config.MyBatisConfig;

public class MemberDAO {
	public SqlSession sqlSession;
	
	public MemberDAO() {
		sqlSession = MyBatisConfig.getSqlSessionFactory().openSession(true);
	}
	
//	회원가입
	public void insert(MemberVO memberVO) {
		sqlSession.insert("member.insert", memberVO);
	}
	
//	로그인
	public Optional<MemberVO> selectByMemberEmailAndMemberPassword(MemberVO memberVO){
		System.out.println((MemberVO) sqlSession.selectOne("member.selectByMemberEmailAndMemberPassword", memberVO));
		return Optional.ofNullable((MemberVO) sqlSession.selectOne("member.selectByMemberEmailAndMemberPassword", memberVO));
	}
}
















