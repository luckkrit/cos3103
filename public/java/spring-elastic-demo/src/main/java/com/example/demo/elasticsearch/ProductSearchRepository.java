package com.example.demo.elasticsearch;

import org.springframework.data.elasticsearch.repository.ElasticsearchRepository;

import java.util.List;

public interface ProductSearchRepository extends ElasticsearchRepository<ProductDocument, String> {

    // Simple derived-query methods work for exact/keyword fields.
    List<ProductDocument> findByProductLine(String productLine);

    List<ProductDocument> findByProductVendor(String productVendor);

}