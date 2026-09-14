package com.example.demo.jpa;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface CustomerRepository extends JpaRepository<CustomerEntity, Long> {

    // Derived query methods (Spring Data writes the SQL automatically)
    Optional<CustomerEntity> findByCustomerNumber(Long customerNumber);

    List<CustomerEntity> findByCountry(String country);

    List<CustomerEntity> findByCityIgnoreCase(String city);

    boolean existsByCustomerNumber(Long customerNumber);
}