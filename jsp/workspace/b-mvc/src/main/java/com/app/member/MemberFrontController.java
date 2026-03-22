package com.app.member;

import java.io.IOException;

import com.app.Result;
import com.app.member.controller.JoinController;
import com.app.member.controller.JoinOkController;
import com.app.member.controller.LoginController;
import com.app.member.controller.LoginOkController;

import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

public class MemberFrontController extends HttpServlet {
	@Override
	protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
		String uri = req.getRequestURI();
		String target = uri.substring(0, uri.lastIndexOf(".")).replace(req.getContextPath(), "");
		Result result = null;
		
		if(target.equals("/join")) {
			result = new JoinController().execute(req, resp);
		} else if(target.equals("/join-ok")) {
			result = new JoinOkController().execute(req, resp);
		} else if(target.equals("/login")) {
			result = new LoginController().execute(req, resp);
		} else if(target.equals("/login-ok")) {
			result = new LoginOkController().execute(req, resp);
		}  
		
		if(result != null) {
			if(result.isRedirect()) {
				resp.sendRedirect(result.getPath());
			}else {
				req.getRequestDispatcher(result.getPath()).forward(req, resp);
			}
		}
		
	}
	
	@Override
	protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
		doGet(req, resp);
	}
}










