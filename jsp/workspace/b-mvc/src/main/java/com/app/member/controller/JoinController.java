package com.app.member.controller;

import java.io.IOException;

import com.app.Action;
import com.app.Result;

import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

public class JoinController implements Action{
	
	@Override
	public Result execute(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
		Result result = new Result();
		
		result.setPath("/member/join.jsp");
		
		return result;
	}
}














