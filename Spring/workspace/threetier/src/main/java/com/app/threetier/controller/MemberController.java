package com.app.threetier.controller;

import com.app.threetier.dto.MemberDTO;
import com.app.threetier.service.member.MemberService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.servlet.view.RedirectView;

@Controller
@RequestMapping("/member/**")
@RequiredArgsConstructor
public class MemberController {
    private final MemberService memberService;

    @GetMapping("check-email")
    @ResponseBody
    public boolean checkEmail(String memberEmail){
        return memberService.checkEmail(memberEmail);
    }

    @GetMapping("join")
    public String goToJoinForm(){
        return "member/join";
    }

    @PostMapping("join")
    public RedirectView join(MemberDTO memberDTO){
        memberService.join(memberDTO);
        return new RedirectView("/member/login");
    }

    @GetMapping("login")
    public String goToLoginForm(){
        return "member/login";
    }

    @PostMapping("login")
    public RedirectView login(MemberDTO memberDTO, Model model){
        model.addAttribute("member", memberService.login(memberDTO));
        return new RedirectView("/post/list");
    }
}










