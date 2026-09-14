package com.example.demo.jpa;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface OrderDetailRepository extends JpaRepository<OrderDetailEntity, OrderDetailId> {

    // orderNumber is one of the @Id fields on OrderDetailEntity, so Spring
    // Data can derive this query directly from the method name - no @Query
    // needed. Returns every line item belonging to that order.
    List<OrderDetailEntity> findByOrderNumber(Integer orderNumber);

    // Returns the next available orderLineNumber for a given order:
    // MAX(existing line numbers) + 1, or 1 if the order has no lines yet.
    @Query("SELECT COALESCE(MAX(od.orderLineNumber) + 1, 1) " +
            "FROM OrderDetailEntity od WHERE od.orderNumber = :orderNumber")
    Integer findNextOrderLineNumber(@Param("orderNumber") Integer orderNumber);

    // Checks whether this exact product already has a line on this order.
    // Since {orderNumber, productCode} is the primary key, this returns
    // at most one row - reuse its line number instead of assigning a new
    // one, and update its quantity instead of inserting a duplicate.
    Optional<OrderDetailEntity> findByOrderNumberAndProductCode(Integer orderNumber, String productCode);
}