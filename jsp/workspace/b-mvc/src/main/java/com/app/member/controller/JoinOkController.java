package com.app.member.controller;

import java.io.IOException;

import com.app.Action;
import com.app.Result;
import com.app.member.domain.MemberVO;
import com.app.member.repository.MemberDAO;

import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

public class JoinOkController implements Action {
	@Override
	public Result execute(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
		Result result = new Result();
		MemberVO memberVO = new MemberVO();
		MemberDAO memberDAO = new MemberDAO();
		
		String memberEmail = req.getParameter("memberEmail");
		String memberPassword = req.getParameter("memberPassword");
		String memberName = req.getParameter("memberName");
		
		memberVO.setMemberEmail(memberEmail);
		memberVO.setMemberPassword(memberPassword);
		memberVO.setMemberName(memberName);
		
		memberDAO.insert(memberVO);
		
		result.setRedirect(true);
		result.setPath(req.getContextPath() + "/login.member");
		
		return result;
	}
}
















