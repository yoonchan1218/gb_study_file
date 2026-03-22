package com.app.ex;

import java.io.IOException;

import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

public class Ex02 extends HttpServlet {
	@Override
	protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
		req.getRequestDispatcher("/ex02.jsp").forward(req, resp);
	}
	
	@Override
	protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
		int number1 =  Integer.parseInt(req.getParameter("number1"));
		int number2 =  Integer.parseInt(req.getParameter("number2"));
		int result = number1 + number2;
		
		resp.sendRedirect(req.getContextPath() + "/ex02-result?number1=" + number1 +"&number2=" + number2 + "&result=" + result);
	}
}

















