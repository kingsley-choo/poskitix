package com.poskitix.cs102.user;

import org.springframework.stereotype.Service;

import java.util.*;

@Service
public class UserService {

    private UserRepository repo;

    public UserService(UserRepository repo) {
        this.repo = repo;
    }

    public List<User> getAllUsers() {
        return repo.findAll();
    }

    public User getUserById(Integer uid) {
        return repo.findByUid(uid).orElseThrow(() -> new IdNotFoundException("User Id not found"));
    }

    public List<User> getUsersByIds(List<Integer> ids) {
        return repo.findByIds(ids).orElseThrow(() -> new IdNotFoundException("One or more user id is not found!"));
    }

    public User saveUser(User user) {
        return repo.save(user);
    }

    public void deleteUserById(int id) {
        repo.deleteById(id);
    }
}
