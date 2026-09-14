package com.example.demo.controller;

import com.example.demo.elasticsearch.ProductDocument;
import com.example.demo.elasticsearch.ProductSearchService;
import com.example.demo.jpa.ProductEntity;
import com.example.demo.jpa.ProductRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestParam;

import java.util.Collections;
import java.util.List;

@Controller
public class ProductSearchController {

    private final ProductSearchService searchService;
    private final ProductRepository productRepository;

    @Autowired
    public ProductSearchController(ProductSearchService searchService,
            ProductRepository productRepository) {
        this.searchService = searchService;
        this.productRepository = productRepository;
    }

    /**
     * Renders the search page for a specific customer/order context.
     * With no query param, shows an empty form. With ?q=..., runs BOTH
     * the Elasticsearch full-text search and a plain SQL LIKE search
     * against Postgres, so the dialog can show them side by side for
     * comparison.
     *
     * customerId and orderNumber come from the URL path (e.g. so links to
     * this page - and links out of it, like the "Order" links - can carry
     * that context forward without needing session state).
     */
    @GetMapping("/product/search/{customerId}/{orderNumber}")
    public String search(@PathVariable Integer customerId,
            @PathVariable Integer orderNumber,
            @RequestParam(name = "q", required = false) String q,
            Model model) {

        List<ProductDocument> results = (q != null && !q.isBlank())
                ? searchService.searchByText(q)
                : Collections.emptyList();

        List<ProductEntity> sqlResults = (q != null && !q.isBlank())
                ? productRepository.searchByNameLike(q)
                : Collections.emptyList();

        model.addAttribute("customerId", customerId);
        model.addAttribute("orderNumber", orderNumber);
        model.addAttribute("query", q);
        model.addAttribute("results", results);
        model.addAttribute("sqlResults", sqlResults);
        model.addAttribute("hasSearched", q != null && !q.isBlank());

        return "products-search"; // resolves to templates/products-search.html
    }
}