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

    /**
     * Exact filter by product line, e.g. "Classic Cars".
     */
    public List<ProductDocument> findByProductLine(String productLine) {
        return repository.findByProductLine(productLine);
    }

    /**
     * Full-text, relevance-ranked search across name and description.
     * Uses the English analyzer set up on ProductDocument, so this matches
     * stemmed variants (e.g. "touring" also matches "tour") and ignores
     * stopwords/case.
     */
    public List<ProductDocument> searchByText(String queryText) {
        Query query = NativeQuery.builder()
                .withQuery(q -> q
                        .multiMatch(m -> m
                                .query(queryText)
                                .fields("productname", "productdescription")
                                .fuzziness("AUTO") // tolerates small typos
                        ))
                .build();

        SearchHits<ProductDocument> hits = operations.search(query, ProductDocument.class);
        return hits.getSearchHits().stream()
                .map(SearchHit::getContent)
                .collect(Collectors.toList());
    }

    /**
     * Autocomplete / search-as-you-type, backed by the completion field.
     * Note: this requires productNameSuggest to actually be populated at
     * index time (see the indexing/sync code) — an empty completion field
     * will never return suggestions.
     */
    public List<String> suggest(String prefix) {
        Query query = NativeQuery.builder()
                .withQuery(q -> q
                        .matchPhrasePrefix(m -> m
                                .field("productNameSuggest")
                                .query(prefix)))
                .build();

        SearchHits<ProductDocument> hits = operations.search(query, ProductDocument.class);
        return hits.getSearchHits().stream()
                .map(hit -> hit.getContent().getProductName())
                .collect(Collectors.toList());
    }

    /**
     * Save or update a single product document (used by the sync path,
     * or for manual re-indexing during development).
     */
    public ProductDocument save(ProductDocument document) {
        return repository.save(document);
    }
}