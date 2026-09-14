package com.example.demo.jpa;

import java.math.BigDecimal;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import jakarta.persistence.Transient;
import lombok.Getter;
import lombok.Setter;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

@Entity
@Table(name = "customers")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class CustomerEntity {

    @Id
    @Column(name = "customernumber")
    private Long customerNumber;

    @Column(name = "customername")
    private String customerName;

    @Column(name = "contactlastname")
    private String contactLastName;

    @Column(name = "contactfirstname")
    private String contactFirstName;

    @Column(name = "phone")
    private String phone;

    @Column(name = "addressline1")
    private String addressLine1;

    @Column(name = "addressline2")
    private String addressLine2;

    @Column(name = "city")
    private String city;

    @Column(name = "state")
    private String state;

    @Column(name = "postalcode")
    private String postalCode;

    @Column(name = "country")
    private String country;

    @Column(name = "salesrepemployeenumber")
    private Integer salesRepEmployeeNumber;

    @Column(name = "creditlimit")
    private BigDecimal creditLimit;

    @Transient
    private String customerLocation;
}