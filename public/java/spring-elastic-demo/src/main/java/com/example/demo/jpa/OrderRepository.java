package com.example.demo.jpa;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface OrderRepository extends JpaRepository<OrderEntity, Integer> {

    List<OrderEntity> findByCustomerNumberOrderByOrderDateDesc(Long customerNumber);

    Optional<OrderEntity> findByOrderNumber(Long orderNumber);
}