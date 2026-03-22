package com.app.ex;

import java.io.IOException;
import java.net.URLEncoder;

import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

public class Ex04 extends HttpServlet{
	@Override
	protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
		req.getRequestDispatcher("/ex04.jsp").forward(req, resp);
	}
	
	@Override
	protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
		String state = req.getParameter("state");
		String city = state.equals("서울") ? "강남구" : "남양주시";
		
		resp.sendRedirect(req.getContextPath() + "/ex04-result?city=" + URLEncoder.encode(city, "UTF-8"));
	}
}

















