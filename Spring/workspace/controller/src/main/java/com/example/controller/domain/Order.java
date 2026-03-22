package com.example.controller.domain;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.ToString;
import org.springframework.web.bind.annotation.GetMapping;
//- 필드: customerName(고객명), productName(상품명),
//          quantity(수량), unitPrice(단가)
//   - 메서드: getTotalPrice() - 총 금액 계산 (수량 * 단가)
@NoArgsConstructor
@Getter @Setter @ToString
public class Order {
    private String customerName;
    private String productName;
    private int quantity;
    private int unitPrice;

    public int getTotalPrice(){
        return unitPrice * quantity;
    }

}
