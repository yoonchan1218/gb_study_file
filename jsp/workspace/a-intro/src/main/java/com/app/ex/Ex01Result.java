package com.app.ex;

import java.io.IOException;

import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

public class Ex01Result extends HttpServlet{
	@Override
	protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
		String memberName = req.getParameter("memberName");
		req.setAttribute("memberName", memberName);
		req.getRequestDispatcher("/ex01-result.jsp").forward(req, resp);
	}
}
