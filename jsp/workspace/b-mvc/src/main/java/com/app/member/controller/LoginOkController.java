package com.app.member.controller;

import java.io.IOException;

import com.app.Action;
import com.app.Result;
import com.app.member.domain.MemberVO;
import com.app.member.repository.MemberDAO;

import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

public class LoginOkController implements Action{
	@Override
	public Result execute(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
		MemberDAO memberDAO = new MemberDAO();
		MemberVO memberVO = new MemberVO();
		
		memberVO.setMemberEmail(req.getParameter("memberEmail"));
		memberVO.setMemberPassword(req.getParameter("memberPassword"));
		
		System.out.println(memberDAO.selectByMemberEmailAndMemberPassword(memberVO).isPresent());
		
		return null;
	}
}

















