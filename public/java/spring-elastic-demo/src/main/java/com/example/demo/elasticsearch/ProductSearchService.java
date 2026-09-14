package com.example.demo.elasticsearch;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.elasticsearch.client.elc.NativeQuery;
import org.springframework.data.elasticsearch.core.ElasticsearchOperations;
import org.springframework.data.elasticsearch.core.SearchHit;
import org.springframework.data.elasticsearch.core.SearchHits;
import org.springframework.data.elasticsearch.core.query.Query;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@Service
public class ProductSearchService {

    private final ProductSearchRepository repository;
    private final ElasticsearchOperations operations;

    @Autowired
    public ProductSearchService(ProductSearchRepository repository, ElasticsearchOperations operations) {
        this.repository = repository;
        this.operations = operations;
    }

    /**
     * Simple lookup by exact product code (the document's @Id).
     */
    public Optional<ProductDocument> findByCode(String productCode) {
        return repository.findById(productCode);
    }

    public List<ProductDocument> searchByText(String queryText) {
        Query query = NativeQuery.builder()
                .withQuery(q -> q
                        .multiMatch(m -> m
                                .query(queryText)
                                .fields("productname", "productdescription")))
                .build();

        SearchHits<ProductDocument> hits = operations.search(query, ProductDocument.class);
        return hits.getSearchHits().stream()
                .map(SearchHit::getContent)
                .collect(Collectors.toList());
    }

}