package com.poskitix.cs102.user;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;
import java.util.List;

@Repository
public interface UserRepository extends JpaRepository<User, Integer> {

    Optional<User> findByUid(Integer uid);

    Optional<List<User>> findByUidIn(List<Integer> uids);

    Optional<User> findByEmail(String email);

    Optional<List<User>> findByEmailIn(List<String> emails);


    // example of custom implementation: find cards by suit
    // List<User> findBySuit(char suit);
}
