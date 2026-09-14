package com.example.demo.jpa;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name = "products")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class ProductEntity {

    @Id
    @Column(name = "productcode", length = 15)
    private String productCode;

    @Column(name = "productname", length = 70)
    private String productName;

}