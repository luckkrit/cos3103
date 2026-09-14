package com.example.demo.jpa;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.LocalDateTime;

@Entity
@Table(name = "orders") // Add schema = "your_schema" if needed
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class OrderEntity {

    @Id
    @Column(name = "ordernumber")
    private Integer orderNumber;

    @Column(name = "orderdate")
    private LocalDateTime orderDate;

    @Column(name = "requireddate")
    private LocalDateTime requiredDate;

    @Column(name = "shippeddate")
    private LocalDateTime shippedDate;

    @Column(name = "status", length = 15)
    private String status;

    @Column(name = "comments", columnDefinition = "text")
    private String comments;

    @Column(name = "customernumber")
    private Long customerNumber;
}