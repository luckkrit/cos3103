package com.example.demo.jpa;

import lombok.*;
import java.io.Serializable;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class OrderDetailId implements Serializable {
    private Integer orderNumber;
    private String productCode;
}