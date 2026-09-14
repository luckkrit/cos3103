package com.example.demo.jpa;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.IdClass;
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.io.Serializable;
import java.math.BigDecimal;

@Entity
@Table(name = "orderdetails")
@IdClass(OrderDetailId.class)
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class OrderDetailsEntity {

    @Id
    @Column(name = "ordernumber")
    private Integer orderNumber;

    @Id
    @Column(name = "productcode", length = 15)
    private String productCode;

    @Column(name = "quantityordered", nullable = false)
    private Integer quantityOrdered;

    @Column(name = "priceeach", nullable = false)
    private BigDecimal priceEach;

    @Column(name = "orderlinenumber", nullable = false)
    private Short orderLineNumber;

}