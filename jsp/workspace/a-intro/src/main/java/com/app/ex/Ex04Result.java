package com.app.ex;

import java.io.IOException;

import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

public class Ex04Result extends HttpServlet{
	@Override
	protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
		String city = req.getParameter("city");
		
		req.setAttribute("city", city);
		req.getRequestDispatcher("/ex04-result.jsp").forward(req, resp);
	}
}




