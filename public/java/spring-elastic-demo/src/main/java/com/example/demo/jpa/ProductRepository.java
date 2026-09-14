package com.example.demo.jpa;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ProductRepository extends JpaRepository<ProductEntity, String> {

    // Plain SQL LIKE - exact substring match only, no typo tolerance,
    // no relevance ranking. Used to demo the contrast against
    // ProductSearchService.searchByText()'s fuzzy Elasticsearch query.
    @Query("SELECT p FROM ProductEntity p WHERE LOWER(p.productName) LIKE LOWER(CONCAT('%', :term, '%'))")
    List<ProductEntity> searchByNameLike(@Param("term") String term);

}