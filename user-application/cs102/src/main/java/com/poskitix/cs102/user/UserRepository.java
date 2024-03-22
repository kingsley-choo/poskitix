package com.poskitix.cs102.user;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface UserRepository extends JpaRepository<User, Integer> {

    Optional<User> findByUid(Integer uid);

    Optional<List<User>> findByIds(List<Integer> ids);
    // example of custom implementation: find cards by suit
//    List<User> findBySuit(char suit);
}
