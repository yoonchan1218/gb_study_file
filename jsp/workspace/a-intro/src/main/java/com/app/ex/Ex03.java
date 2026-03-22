package com.app.ex;

import java.io.IOException;
import java.net.URLEncoder;

import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

public class Ex03 extends HttpServlet {
	@Override
	protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
		req.getRequestDispatcher("/ex03.jsp").forward(req, resp);
	}
	
	@Override
	protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
		String fruitName = req.getParameter("fruitName");
		String fruitPrice = req.getParameter("fruitPrice");
		
		resp.sendRedirect(req.getContextPath() + "/ex03-result?fruitName=" + URLEncoder.encode(fruitName, "UTF-8") + "&fruitPrice=" + fruitPrice);
	}
}
















