package com.example.demo.controller;

import com.example.demo.elasticsearch.ProductDocument;
import com.example.demo.elasticsearch.ProductSearchService;
import com.example.demo.jpa.OrderDetailEntity;
import com.example.demo.jpa.OrderDetailRepository;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;

import java.math.BigDecimal;
import java.util.List;
import java.util.Optional;

@Controller
public class OrderDetailsController {

    private final OrderDetailRepository orderDetailRepo;

    private final ProductSearchService productSearchService;

    public OrderDetailsController(OrderDetailRepository orderDetailRepo, ProductSearchService searchService) {
        this.orderDetailRepo = orderDetailRepo;
        this.productSearchService = searchService;
    }

    @GetMapping("/orderdetails/{customerId}/{orderNumber}")
    public String showOrderDetails(@PathVariable Integer customerId,
            @PathVariable Integer orderNumber,
            Model model) {

        List<OrderDetailEntity> details = orderDetailRepo.findByOrderNumber(orderNumber);

        model.addAttribute("customerId", customerId);
        model.addAttribute("orderNumber", orderNumber);
        model.addAttribute("details", details);

        return "orderdetails-form"; // loads templates/index.html
    }

    @GetMapping("/orderdetails/update/{customerId}/{orderNumber}/{productCode}/{quantity}")
    public String updateOrderDetails(@PathVariable Integer customerId,
            @PathVariable Integer orderNumber,
            @PathVariable String productCode,
            @PathVariable Integer quantity,
            Model model) {

        Optional<OrderDetailEntity> existing = orderDetailRepo.findByOrderNumberAndProductCode(orderNumber,
                productCode);

        if (existing.isPresent()) {
            // Same product already on this order - update its quantity instead
            // of adding a new line, and keep its existing orderLineNumber.
            OrderDetailEntity detail = existing.get();
            if (detail.getQuantityOrdered() + quantity == 0) {
                orderDetailRepo.delete(detail);
            } else {
                detail.setQuantityOrdered(detail.getQuantityOrdered() + quantity);
                orderDetailRepo.save(detail);
            }
        } else {
            // New product for this order - assign the next line number.
            Integer nextLine = orderDetailRepo.findNextOrderLineNumber(orderNumber);
            OrderDetailEntity newDetail = new OrderDetailEntity();
            newDetail.setOrderNumber(orderNumber);
            newDetail.setProductCode(productCode);
            newDetail.setOrderLineNumber(nextLine.shortValue());
            newDetail.setQuantityOrdered(quantity);
            ProductDocument product = productSearchService.findByCode(productCode)
                    .orElseThrow(() -> new IllegalArgumentException("Unknown product: " + productCode));
            newDetail.setPriceEach(BigDecimal.valueOf(product.getBuyPrice()));
            orderDetailRepo.save(newDetail);
        }

        List<OrderDetailEntity> details = orderDetailRepo.findByOrderNumber(orderNumber);
        model.addAttribute("customerId", customerId);
        model.addAttribute("orderNumber", orderNumber);
        model.addAttribute("details", details);

        return "orderdetails-form"; // loads templates/index.html
    }
}
