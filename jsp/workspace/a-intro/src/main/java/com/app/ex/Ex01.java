package com.app.ex;

import java.io.IOException;
import java.net.URLEncoder;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

public class Ex01 extends HttpServlet{
	@Override
	protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
		req.getRequestDispatcher("/ex01.jsp").forward(req, resp);
	}
	
	@Override
	protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
		StringBuilder stringBuilder = new StringBuilder();
		String memberName = req.getParameter("memberName");
		
		stringBuilder.append(memberName);
		stringBuilder.append("님");
		
		memberName = stringBuilder.toString();

		resp.sendRedirect(req.getContextPath() + "/ex01-result?memberName=" + URLEncoder.encode(memberName, "UTF-8"));
	}
}















