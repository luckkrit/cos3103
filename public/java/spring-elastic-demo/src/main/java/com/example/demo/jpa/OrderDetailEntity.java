// OrderDetailEntity.java
package com.example.demo.jpa;

import jakarta.persistence.*;
import lombok.*;
import java.math.BigDecimal;

@Entity
@Table(name = "orderdetails")
@IdClass(OrderDetailId.class)
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class OrderDetailEntity {

    @Id
    @Column(name = "ordernumber")
    private Integer orderNumber;

    @Id
    @Column(name = "productcode", length = 15)
    private String productCode;

    @Column(name = "quantityordered", nullable = false)
    private Integer quantityOrdered;

    @Column(name = "priceeach", nullable = false, precision = 10, scale = 2)
    private BigDecimal priceEach;

    @Column(name = "orderlinenumber", nullable = false)
    private Short orderLineNumber;
}